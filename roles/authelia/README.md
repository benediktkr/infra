# authelia

## password reset token expiration

the expiration time for a password reset token in authelia is
hardcoded to be 5 minutes, which has repeated caused problems and
confusion with some users.

deploying a custom build with longer expiration times would be possible, here
is a diff for that (using 3 days as an example, which quite a lot):

```git
diff --git a/internal/model/identity_verification.go b/internal/model/identity_verification.go
index f0f58bc4..25643697 100644
--- a/internal/model/identity_verification.go
+++ b/internal/model/identity_verification.go
@@ -13,7 +13,8 @@ func NewIdentityVerification(jti uuid.UUID, username, action string, ip net.IP)
 	return IdentityVerification{
 		JTI:       jti,
 		IssuedAt:  time.Now(),
-		ExpiresAt: time.Now().Add(5 * time.Minute),
+                // 4320 minutes = 3 days
+		ExpiresAt: time.Now().Add(4320 * time.Minute),
 		Action:    action,
 		Username:  username,
 		IssuedIP:  NewIP(ip),
```

## tokens in the database

the password reset tokens and their expiration times are stored in the
table `identity_verification` (it is also used for other things, such as
TOPT device resets)

field         | description
--------------|------------
`id`          | incremental id (int)
`jti`         | an uuid
`iat`         | creation time
`issued_ip`   | client ip
`exp`         | expiration time
`username`    | the username (or email, as entered in the password reset dialog)
`action`      | the action taken. examples: `ResetPassword`, `ResetTOTPDevice`
`consumed`    | timestamp of when it was used, `NULL` if it was never used.
`consumed_ip` | client ip

query to list all unused password reset tokens:

```sql
select id, jti, exp, username
from identity_verification
where consumed is NULL and action="ResetPassword"\G
```

## changing the expiry time

first a password reset for `$username` has to be requested. then you
can find it in the database:

```sql
select id, exp
from identity_verification
where consumed is NULL and action="ResetPassword" and username="$username"
```

or just get the latest row

```sql
select id, exp
from identity_verification
where consumed is NULL and action="ResetPassword" and username="$username"
order by id desc limit 1
```

and then update row `$id` with a timestamp in ISO format:

```sql
update identity_verification
set exp="2022-09-16 12:15:00" where id=$id;
```

## do it in one query

with a subquery:

```sql
update identity_verification
set exp="2022-09-17 12:15:00"
where id=(
    select id
    from identity_verification
    where consumed is NULL and action="ResetPassword" and username="$username"
    order by id desc limit 1
);
```

without a subquery:

```sql
update identity_verification
set exp="2022-09-18 12:15:00"
where consumed is NULL and action="ResetPassword" and username="$username"
and iat>CURDATE();
```

it works with `CURDATE` if the password reset was requested today, but
the subquery is probably less prone to error (for example if it was requested
at 23:59, and you run the subquery at 00:01, it would not match).

i'll probably write a small script for this and update this document
with info about the script (but not removing the sql examples).
