const std = @import("std");

// sample test

const test_link: []const u8 = "https://tinyurl.com/yh5p26n3";
// const test_link: []const u8 = "http://github.com/ezxd1148";
//const test_link: []const u8 = "notavalidlink";
// const test_link: []const u8 = "https://www.github.com";

// data

const ALLOWED_SCHEMES = [_][]const u8{ "http", "https" };

// processing

pub fn normalizeLink(link: []const u8) !usize {
    // return 0 if link is valid, error code otherwise

    // parse link into a Uri struct
    const parsed = std.Uri.parse(link) catch |e| {
        std.debug.print("Failed to parse link: {any}\n\n", .{e});
        std.debug.print("Please enter valid URL\n\n", .{});
        return error.InvalidLink;
    };

    // print entire URL
    std.debug.print("Parsed: {any}\n\n", .{parsed});

    const urlScheme = parsed.scheme;
    // print parsed URL scheme
    std.debug.print("Scheme: {s}\n\n", .{urlScheme});

    var i: usize = 0;
    // check if scheme is allowed
    for (ALLOWED_SCHEMES) |scheme| {
        if (std.mem.eql(u8, urlScheme, scheme)) {
            std.debug.print("Scheme is allowed: {s}\n\n", .{scheme});
            break;
        } else if (i == ALLOWED_SCHEMES.len - 1) {
            std.debug.print("Scheme is NOT allowed: {s}\n\n", .{urlScheme});
            return error.InvalidScheme;
        }
        i += 1;
    }

    var buf: [std.Io.net.HostName.max_len]u8 = undefined;
    const getHost = try std.Uri.getHost(parsed, &buf);

    // print parsed URL host
    std.debug.print("Host: {s}\n\n", .{getHost.bytes});

    // check if host is ip address

    _ = std.Io.net.IpAddress.parse(getHost.bytes, 0) catch {
        std.debug.print("Host is not IP address\n\n", .{});
    };

    if (std.Io.net.IpAddress.parse(getHost.bytes, 0)) |a| {
        std.debug.print("Host is IP address: {any}\n\n", .{a});
        return error.InvalidHost;
    } else |err| {
        std.debug.print("Host is not IP address: {any}\n\n", .{err});
    }

    // check if username and password is present

    if (parsed.user != null) {
        std.debug.print("Username is present\n\n", .{});
        return error.InvalidUsername;
    } else {
        std.debug.print("Username not present\n\n", .{});
    }
    if (parsed.password != null) {
        std.debug.print("Password is present\n\n", .{});
        return error.InvalidPassword;
    } else {
        std.debug.print("Password not present\n\n", .{});
    }

    const urlPath = parsed.path;
    // print parsed URL path
    std.debug.print("Path: {s}\n\n", .{urlPath.percent_encoded});

    // print parsed URL query
    std.debug.print("Query: {any}\n\n", .{parsed.query});

    return 0;
}

pub fn resolveLink(link: []const u8, client: *std.http.Client) !std.http.Client.Response {
    var redirect_buffer: [8224]u8 = undefined;

    // get uri from link
    const linkUri = try std.Uri.parse(link);

    var request = try client.request(.GET, linkUri, .{ .keep_alive = false });
    defer request.deinit();

    const response = try request.receiveHead(&redirect_buffer);

    return response;
}

// init
pub fn main(init: std.process.Init) !void {
    _ = init;
    //const io = init.io;
    //const allocator = init.gpa;

    //var client = std.http.Client{
    //    .allocator = allocator,
    //    .io = io,
    //};

    if (try normalizeLink(test_link) == 0) {
        std.debug.print("Link is valid\n\n", .{});
    } else {
        _ = normalizeLink(test_link) catch |err| {
            switch (err) {
                error.InvalidScheme => std.debug.print("Invalid scheme\n\n", .{}),
                error.InvalidHost => std.debug.print("Invalid host\n\n", .{}),
                error.InvalidUsername => std.debug.print("Invalid username\n\n", .{}),
                error.InvalidPassword => std.debug.print("Invalid password\n\n", .{}),
                else => std.debug.print("Unknown error: {any}\n\n", .{err}),
            }
        };
    }

    // const resolve = try resolveLink(test_link, &client);

    // std.debug.print("{any}\n\n", .{resolve});
}
